import React, { useState } from "react";
import AuthRequired from "../../components/auth/AuthRequired";
import ChatBody from "../../components/chatbody/ChatBody";
import Sidebar from "../../components/sidebar/sidebar";

const HomeScreen = (props) => {
    const [currentChattingMember, setCurrentChattingMember] = useState({});
    const [onlineUserList, setOnlineUserList] = useState([]);

    return (
        <main>
            <div>
                <div>
                    <div>
                        <Sidebar
                            setCurrentChattingMember={setCurrentChattingMember}
                            onlineUserList={onlineUserList}
                            {...props}
                        />
                        <ChatBody
                            setOnlineUserList={setOnlineUserList}
                            currentChattingMember={currentChattingMember}
                            {...props}
                        />
                    </div>
                </div>
            </div>
        </main>
    );
};

export default AuthRequired(HomeScreen);
