import React, { useRef } from "react";

const Modal = ({ modalCloseHandler, show, children }) => {
    const modalBodyRef = useRef();

    const modalOutsideClickHandler = (event) => {
        if (!modalBodyRef.current.contains(event.target)) {
            modalCloseHandler();
        }
    };

    return (
        <div
            onClick={modalOutsideClickHandler}
            style={show ? { display: "block" } : { display: "none" }}
        >
            <section ref={modalBodyRef}>
                <div>
                    <span
                        onClick={modalCloseHandler}
                        aria-hidden="true"
                    >
                        ×
                    </span>
                </div>
                <div>{children}</div>
            </section>
        </div>
    );
};

export default Modal;
