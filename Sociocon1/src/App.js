import './App.css';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from './Home';
import Login from './Login';
import Profile from './Profile';
import Inbox from './Inbox';
import {Provider} from "react-redux";
import "./App.css";
import store, {persistor} from "./store";
import {PersistGate} from "redux-persist/integration/react";


function App() {
  return (
    // bem
      <Provider store={store}>
          <PersistGate persistor={persistor} loading={null}>

              <Router>
                  <div className="app">
                      {/* link: https://www.youtube.com/watch?v=Ul3y1LXxzdU
            author: https://www.youtube.com/c/WebDevSimplified
            License: https://creativecommons.org/choose/ */}

                      <Routes>
                          <Route path = "/" element = {<Home/>} />
                          <Route path = "/login" element = {<Login/>} />
                          <Route path = "/profile" element = {<Profile/>} />
                          <Route path = "/inbox" element = {<Inbox/>} />
                      </Routes>



                  </div>


              </Router>
          </PersistGate>
      </Provider>


  );
}

export default App;
