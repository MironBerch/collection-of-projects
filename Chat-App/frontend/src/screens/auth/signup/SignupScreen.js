import React, { useRef } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import ApiConnector from "../../../api/apiConnector";
import ApiEndpoints from "../../../api/apiEndpoints";
import AppPaths from "../../../lib/appPaths";

const SignupScreen = ({ history }) => {
    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
    } = useForm();
    const password = useRef({});
    password.current = watch("password");
    const image = watch("image");

    const onSubmit = async (signupData) => {
        const formData = new FormData();
        formData.append("image", signupData.image[0]);
        delete signupData["image"];
        Object.keys(signupData).forEach((key) => {
            formData.append(key, signupData[key]);
        });
        const successSignupData = await ApiConnector.sendPostRequest(
            ApiEndpoints.SIGN_UP_URL,
            formData,
            false,
            true
        );
        if (successSignupData) {
            history.push({
                pathname: AppPaths.LOGIN,
                state: { redirectFrom: AppPaths.SIGN_UP },
            });
        }
    };

    return (
        <div id="authFormContainer">
            <div id="authForm">
                <h2 id="authTitle">Sign Up</h2>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div>
                        <input
                            type="text"
                            placeholder="First Name"
                            {...register("first_name", { required: true })}
                        />
                        {errors.first_name && (
                            <p>This field is required</p>
                        )}
                    </div>
                    <div>
                        <input
                            type="text"
                            placeholder="Last Name"
                            {...register("last_name", { required: true })}
                        />
                        {errors.last_name && (
                            <p>This field is required</p>
                        )}
                    </div>
                    <div>
                        <input
                            type="email"
                            placeholder="Email"
                            {...register("email", { required: true })}
                        />
                        {errors.email && (
                            <p>This field is required</p>
                        )}
                    </div>
                    <div>
                        <input
                            type="file"
                            name="image"
                            id="validatedCustomFile"
                            {...register("image", {
                                required: true,
                            })}
                        />
                        <label htmlFor="validatedCustomFile">
                            {image ? image[0]?.name : "Choose Image..."}
                        </label>
                        {errors.image && (
                            <p>This field is required</p>
                        )}
                    </div>
                    <div>
                        <input
                            type="password"
                            placeholder="Password"
                            {...register("password", { required: true })}
                        />
                        {errors.password && (
                            <p>This field is required</p>
                        )}
                    </div>
                    <div>
                        <input
                            type="password"
                            name="confirm_password"
                            placeholder="Confirm Password"
                            {...register("confirm_password", {
                                required: "This field is required",
                                validate: (value) =>
                                    value === password.current || "The passwords doesn't match",
                            })}
                        />
                        {errors.confirm_password && (
                            <p className="confirm_password">
                                {errors.confirm_password?.message}
                            </p>
                        )}
                    </div>
                    <br />
                    <button type="submit">
                        Sign Up
                    </button>
                </form>
                <p id="authFormFooter">
                    Already have an account. <Link to="/login">Click here</Link> to login.
                </p>
            </div>
        </div>
    );
};

export default SignupScreen;
