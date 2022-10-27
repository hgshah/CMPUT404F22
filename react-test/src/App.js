import {Route, Routes} from "react-router-dom";
import "./App.css";
import Nav from "./components/Nav";
import Home from "./page/Home";
import Profile from "./page/Profile";
import Inbox from "./page/Inbox";
import {Provider} from "react-redux";
import store, {persistor} from "./store";
import {PersistGate} from "redux-persist/integration/react";


function App() {
    return (
        <Provider store={store}>
            <PersistGate persistor={persistor} loading={null}>
                <div className='app'>
                    <Nav/>
                    <Routes>
                        <Route path="/" element={<Home/>}/>
                        <Route path="/profile" element={<Profile/>}/>

                        {/* Approach #2 */}
                        <Route path="inbox/*" element={<Inbox/>}/>

                        <Route path="*" element={<NotFound/>}/>
                    </Routes>
                </div>
            </PersistGate>
        </Provider>
    );
}

export const NotFound = () => {
    return <div><h1> 404 page not found </h1></div>
}

export default App;
