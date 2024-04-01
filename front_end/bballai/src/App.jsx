import TeamCard from "./components/TeamCards"
import Nav from "./components/Nav"
import Main from "./components/Main"

import TeamInfo from "./components/TeamInfo"


function App() {
  const nav_list = ['matchups','teams', 'players','news','predictions','standings','schedule','leaders','stats','scores']

  


  return (
    <div className="wrapper">
      <Nav nav_list = {nav_list}/>
      <TeamInfo />
      <TeamCard/>
      <Main/>

      {/* <ProfileCard/> */}
    </div>
  )
}

export default App
