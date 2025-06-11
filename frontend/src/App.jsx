import {Routes, Route} from 'react-router-dom';
import Listings from './pages/Listings';
import Navbar from './components/Navbar';

function App() {

  return (
    <>
      <Navbar className="pb-5"></Navbar>
      <div className="pt-18">
        <Routes>
          <Route path="/" element={<Listings></Listings>}></Route>
        </Routes>
      </div>
    </>
  )
}

export default App
