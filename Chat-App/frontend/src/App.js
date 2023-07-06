import React, { Component } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomeScreen from './screens/home/HomeScreen';
import LoginScreen from './screens/auth/login/LoginScreen';
import SignupScreen from './screens/auth/signup/SignupScreen';
import AppPaths from './lib/appPaths';

export default class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <Routes>
                    <Route path={AppPaths.HOME} exact element={<HomeScreen />} />
                    <Route path={AppPaths.CHAT_ROOM} exact element={<HomeScreen />} />
                    <Route path={AppPaths.LOGIN} exact element={<LoginScreen />} />
                    <Route path={AppPaths.SIGN_UP} exact element={<SignupScreen />} />
                </Routes>
            </BrowserRouter>
        );
    }
}
