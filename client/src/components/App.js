import React, {useState} from "react";
import {Container} from "reactstrap";
import {HomePage} from "./homePage/homePage";
import {ApiService} from "./ApiService";

export default function App() {
    const apiService = new ApiService()
    const [state, setState] = useState(BLANK_STATE);
    const [data, setData] = useState(null);

    let healthCheck = () => {
        apiService.healthCheck().then((status) => {
            initialize(status);
        });
    };

    let getUsers = () => {
        apiService.getUsers().then((data) => {
            setData(data)
        });
    };
    let initialize = (status) => {
        setState(status);
    };

    if (state === BLANK_STATE) {
        healthCheck()
    }

    return (
        <div>
            <Container>
                <HomePage okStatus={state.status}/>
            </Container>
            <Container>
                    <h1>API Call Button Example</h1>
                    <button onClick={getUsers}>GetUsers</button>
                    {data && (
                        <div>
                            <h2>Users:</h2>
                            <pre>{JSON.stringify(data, null, 2)}</pre>
                        </div>
                    )}
            </Container>
        </div>
    );
}

const BLANK_STATE = {
    status: ""
};
