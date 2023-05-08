import React, { useState, useEffect} from 'react';
import TodoView from './components/TodoListView';
import axios from 'axios';

function App() {
    const [todoList, setTodoList] = useState([{}])
    const [title, setTitle] = useState('') 
    const [desc, setDesc] = useState('')
    // Read all todos
    useEffect(() => {
        axios.get('http://localhost:8000/api/todo')
        .then(res => {
            setTodoList(res.data)
        })
    });

  // Post a todo
    const addTodoHandler = () => {
        axios.post('http://localhost:8000/api/todo/', { 'title': title, 'description': desc })
        .then(res => console.log(res))
    };

    return (
        <div>
            <h1>Task Manager</h1>
            <h6>FASTAPI - React - MongoDB</h6>
            <div>
                <h5>Add Your Task</h5>
                <span> 
                    <input onChange={event => setTitle(event.target.value)} placeholder='Title'/> 
                    <input onChange={event => setDesc(event.target.value)}   placeholder='Description'/>
                    <button onClick={addTodoHandler}>Add Task</button>
                </span>
                <h5>Your Tasks</h5>
                <div>
                    <TodoView todoList={todoList} />
                </div>
            </div>
        </div>
    );
}

export default App;
