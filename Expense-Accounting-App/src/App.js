import React, { useState } from "react";
import NewCost from "./components/NewCost/NewCost";
import Costs from "./components/Costs/Costs";


const INITIAL_COSTS = [
    {
        id: "c2",
        date: new Date(2023, 11, 25),
        description: "MacBook",
        amount: 1254.72,
    },
];

const App = () => {
    const [costs, setCosts] = useState(INITIAL_COSTS);

    const addCostHandler = (cost) => {
        setCosts((prevCosts) => {
        return [cost, ...prevCosts];
        });
    };

    return (
        <div>
        <NewCost onAddCost={addCostHandler} />
        <Costs costs={costs} />
        </div>
    );
};

export default App;