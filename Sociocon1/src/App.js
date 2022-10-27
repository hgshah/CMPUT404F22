import './App.css';
import Sidebar from './Sidebar';
import Feed from './Feed';
import News from './News';
import {Provider} from "react-redux";
import "./App.css";
import store, {persistor} from "./store";
import {PersistGate} from "redux-persist/integration/react";

function App() {
    return (
        // bem
        <Provider store={store}>
            <PersistGate persistor={persistor} loading={null}>
                <div className="app">
                    {/*side bar */}
                    <Sidebar/>

                    {/*feed */}
                    <Feed/>
                    {/*widgets */}
                    <News/>
                </div>
            </PersistGate>
        </Provider>
    );
}

export default App;
