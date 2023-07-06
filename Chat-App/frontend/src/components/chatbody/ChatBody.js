import React, { useEffect, useState } from "react";
import ApiConnector from "../../api/apiConnector";
import ApiEndpoints from "../../api/apiEndpoints";
import ServerUrl from "../../api/serverUrl";
import Constants from "../../lib/constants";
import SocketActions from "../../lib/socketActions";
import CommonUtil from "../../util/commonUtil";

let socket = new WebSocket(
    ServerUrl.WS_BASE_URL + `ws/users/${CommonUtil.getUserId()}/chat/`
);
let typingTimer = 0;
let isTypingSignalSent = false;

const ChatBody = ({ match, currentChattingMember, setOnlineUserList }) => {
    const [inputMessage, setInputMessage] = useState("");
    const [messages, setMessages] = useState({});
    const [typing, setTyping] = useState(false);

    const fetchChatMessage = async () => {
        const currentChatId = CommonUtil.getActiveChatId(match);
        if (currentChatId) {
            const url =
                ApiEndpoints.CHAT_MESSAGE_URL.replace(
                    Constants.CHAT_ID_PLACE_HOLDER,
                    currentChatId
                ) + "?limit=20&offset=0";
            const chatMessages = await ApiConnector.sendGetRequest(url);
            setMessages(chatMessages);
        }
    };

    useEffect(() => {
        fetchChatMessage();
    }, [CommonUtil.getActiveChatId(match)]);

    const loggedInUserId = CommonUtil.getUserId();
    const getChatMessageClassName = (userId) => {
        return loggedInUserId === userId
            ? "chat-message-right pb-3"
            : "chat-message-left pb-3";
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const chatId = CommonUtil.getActiveChatId(match);
        const userId = CommonUtil.getUserId();
        if (chatId === data.roomId) {
            if (data.action === SocketActions.MESSAGE) {
                data["userImage"] = ServerUrl.BASE_URL.slice(0, -1) + data.userImage;
                setMessages((prevState) => {
                    let messagesState = JSON.parse(JSON.stringify(prevState));
                    messagesState.results.unshift(data);
                    return messagesState;
                });
                setTyping(false);
            } else if (data.action === SocketActions.TYPING && data.user !== userId) {
                setTyping(data.typing);
            }
        }
        if (data.action === SocketActions.ONLINE_USER) {
            setOnlineUserList(data.userList);
        }
    };

    const messageSubmitHandler = (event) => {
        event.preventDefault();
        if (inputMessage) {
            socket.send(
                JSON.stringify({
                    action: SocketActions.MESSAGE,
                    message: inputMessage,
                    user: CommonUtil.getUserId(),
                    roomId: CommonUtil.getActiveChatId(match),
                })
            );
        }
        setInputMessage("");
    };

    const sendTypingSignal = (typing) => {
        socket.send(
            JSON.stringify({
                action: SocketActions.TYPING,
                typing: typing,
                user: CommonUtil.getUserId(),
                roomId: CommonUtil.getActiveChatId(match),
            })
        );
    };

    const chatMessageTypingHandler = (event) => {
        if (event.keyCode !== Constants.ENTER_KEY_CODE) {
            if (!isTypingSignalSent) {
                sendTypingSignal(true);
                isTypingSignalSent = true;
            }
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                sendTypingSignal(false);
                isTypingSignalSent = false;
            }, 3000);
        } else {
            clearTimeout(typingTimer);
            isTypingSignalSent = false;
        }
    };

    return (
        <div>
            <div>
                <div>
                    <div>
                        <img
                            src={currentChattingMember?.image}
                            alt="User"
                            width="40"
                            height="40"
                        />
                    </div>
                    <div>
                        <strong>{currentChattingMember?.name}</strong>
                    </div>
                </div>
            </div>
            <div>
                <div id="chat-message-container">
                    {typing && (
                        <div>
                            <div className="typing">...</div>
                        </div>
                    )}
                    {messages?.results?.map((message, index) => (
                        <div key={index} className={getChatMessageClassName(message.user)}>
                            <div>
                                <img
                                    src={message.userImage}
                                    alt={message.userName}
                                    width="40"
                                    height="40"
                                />
                                <div>
                                    {CommonUtil.getTimeFromDate(message.timestamp)}
                                </div>
                            </div>
                            <div>
                                <div>{message.userName}</div>
                                {message.message}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <div>
                <form onSubmit={messageSubmitHandler}>
                    <div>
                        <input
                            onChange={(event) => setInputMessage(event.target.value)}
                            onKeyUp={chatMessageTypingHandler}
                            value={inputMessage}
                            id="chat-message-input"
                            type="text"
                            placeholder="Type your message"
                            autoComplete="off"
                        />
                        <button id="chat-message-submit">Send</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ChatBody;
