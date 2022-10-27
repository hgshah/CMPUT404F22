import './App.css';
import Sidebar from './Sidebar';
import Feed from './Feed';
import News from './News';
function App() {
  return (
    // bem
    <div className="app">
      {/*side bar */}
      <Sidebar />

      {/*feed */}
      <Feed />
      {/*widgets */}
      <News />
    </div>
  );
}

export default App;
