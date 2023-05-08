import axios from 'axios'
import React from 'react'

function TodoItem(props) {
    const deleteTodoHandler = (title) => {
    axios.delete(`http://localhost:8000/api/todo/${title}`)
        .then(res => console.log(res.data)) }

    return (
        <div>
            <p>
                <span>{props.todo.title} : </span> {props.todo.description} 
                <button onClick={() => deleteTodoHandler(props.todo.title)}>X</button>
                <hr></hr>
            </p>
        </div>
    )
}

export default TodoItem;
