import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import CookieUtil from "../../util/cookieUtil";
import AppPaths from "../../lib/appPaths";
import ApiConnector from "../../api/apiConnector";
import ApiEndpoints from "../../api/apiEndpoints";
import CommonUtil from "../../util/commonUtil";
import Constants from "../../lib/constants";
import Modal from "../modal/modal";

const Sidebar = (props) => {
    const [chatUsers, setChatUsers] = useState([]);
    const [users, setUsers] = useState([]);
    const [isShowAddPeopleModal, setIsShowAddPeopleModal] = useState(false);

    const redirectUserToDefaultChatRoom = (chatUsers) => {
        if (props?.location?.pathname === AppPaths.HOME) {
            props.setCurrentChattingMember(chatUsers[0]);
            props.history.push("/c/" + chatUsers[0].roomId);
        } else {
            const activeChatId = CommonUtil.getActiveChatId(props.match);
            const chatUser = chatUsers.find((user) => user.roomId === activeChatId);
            props.setCurrentChattingMember(chatUser);
        }
    };

    const fetchChatUser = async () => {
        const url = ApiEndpoints.USER_CHAT_URL.replace(
            Constants.USER_ID_PLACE_HOLDER,
            CommonUtil.getUserId()
        );
        const chatUsers = await ApiConnector.sendGetRequest(url);
        const formatedChatUser = CommonUtil.getFormatedChatUser(
            chatUsers,
            props.onlineUserList
        );
        setChatUsers(formatedChatUser);
        redirectUserToDefaultChatRoom(formatedChatUser);
    };

    useEffect(() => {
        fetchChatUser();
    }, []);

    const getConnectedUserIds = () => {
        let connectedUsers = "";
        for (let chatUser of chatUsers) {
            connectedUsers += chatUser.id + ",";
        }
        return connectedUsers.slice(0, -1);
    };

    const fetchUsers = async () => {
        const url = ApiEndpoints.USER_URL + "?exclude=" + getConnectedUserIds();
        const users = await ApiConnector.sendGetRequest(url);
        setUsers(users);
    };

    const addPeopleClickHandler = async () => {
        await fetchUsers();
        setIsShowAddPeopleModal(true);
    };

    const addMemberClickHandler = async (memberId) => {
        const userId = CommonUtil.getUserId();
        let requestBody = {
            members: [memberId, userId],
            type: "DM",
        };
        await ApiConnector.sendPostRequest(
            ApiEndpoints.CHAT_URL,
            JSON.stringify(requestBody),
            true,
            false
        );
        fetchChatUser();
        setIsShowAddPeopleModal(false);
    };

    const getActiveChatClass = (roomId) => {
        let activeChatId = CommonUtil.getActiveChatId(props.match);
        return roomId === activeChatId ? "active-chat" : "";
    };

    const logoutClickHandler = () => {
        CookieUtil.deleteCookie(Constants.ACCESS_PROPERTY);
        CookieUtil.deleteCookie(Constants.REFRESH_PROPERTY);
        window.location.href = AppPaths.LOGIN;
    };

    const getChatListWithOnlineUser = () => {
        let updatedChatList = chatUsers.map((user) => {
            if (props.onlineUserList.includes(user.id)) {
                user.isOnline = true;
            } else {
                user.isOnline = false;
            }
            return user;
        });
        return updatedChatList;
    };

    return (
        <div>
            <div>
                <button onClick={addPeopleClickHandler}>Add People</button>
            </div>
            <div>
                {getChatListWithOnlineUser()?.map((chatUser) => {
                    return (
                        <Link
                            onClick={() => props.setCurrentChattingMember(chatUser)}
                            to={`/c/${chatUser.roomId}`}
                            className={getActiveChatClass(chatUser.roomId)}
                            key={chatUser.id}
                        >
                            <div>
                                <img
                                    src={chatUser.image}
                                    alt={chatUser.name}
                                    width="40"
                                    height="40"
                                />
                                <div>
                                    {chatUser.name}
                                    <div>{chatUser.isOnline ? (<>Online</>) : (<>offline</>)}</div>
                                </div>
                            </div>
                        </Link>
                    );
                })}
            </div>
            <button onClick={logoutClickHandler}>Log Out</button>
            <hr />
            <Modal
                modalCloseHandler={() => setIsShowAddPeopleModal(false)}
                show={isShowAddPeopleModal}
            >
                {users.length > 0 ? (
                    users?.map((user) => (
                        <div key={user.id}>
                            <img
                                src={user.image}
                                alt={user.first_name + " " + user.last_name}
                                width="40"
                                height="40"
                            />
                            <div>{user.first_name + " " + user.last_name}</div>
                            <button onClick={() => addMemberClickHandler(user.id)}>Add</button>
                        </div>
                    ))
                ) : (
                    <h3>No More User Found</h3>
                )}
            </Modal>
        </div>
    );
};

export default Sidebar;
