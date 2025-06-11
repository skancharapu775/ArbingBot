import {Routes, Route} from 'react-router-dom';
import Listings from './pages/Listings';
import HowItWorks from './pages/HowItWorks';
import Navbar from './components/Navbar';

function App() {

  return (
    <>
      <Navbar className="pb-5"></Navbar>
      <div className="pt-18">
        <Routes>
          <Route path="/" element={<Listings></Listings>}></Route>
          <Route path="/how-it-works" element={<HowItWorks></HowItWorks>}></Route>
        </Routes>
      </div>
    </>
  )
}

export default App
