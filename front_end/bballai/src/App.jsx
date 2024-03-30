import Sidebar from "./components/Sidebar"
import Header from "./components/Header"
import Main from "./components/Main"
import Nav from "./components/Nav"


function App() {
  const nav_list = ['matchups','teams', 'players','news','predictions','standings','schedule','leaders','stats','scores']

  


  return (
    <div className="container">
      <Header nav_list = {nav_list}/>
      <Main/>
      <Sidebar/>
      {/* <ProfileCard/> */}
    </div>
  )
}

export default App
