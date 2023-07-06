import React from "react";
import { Navigate } from "react-router-dom";
import AppPaths from "../../lib/appPaths";
import Constants from "../../lib/constants";
import CookieUtil from "../../util/cookieUtil";

const AuthRequired = (Component) => {
    return class AuthenticatedComponent extends React.Component {
        render() {
            if (CookieUtil.getCookie(Constants.ACCESS_PROPERTY)) {
                return <Component {...this.props} />;
            }
            return <Navigate to={AppPaths.LOGIN} />;
        }
    };
};

export default AuthRequired;
