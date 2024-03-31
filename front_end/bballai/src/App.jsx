import Sidebar from "./components/Sidebar"
import Header from "./components/Header"
import Main from "./components/Main"
import phili from './to_use.png'


function App() {
  const nav_list = ['matchups','teams', 'players','news','predictions','standings','schedule','leaders','stats','scores']

  


  return (
    <div className="container">
      <Header nav_list = {nav_list}/>
      <div className='team-info'>
             <div className=" team-stats-table-div">
                   <table className="team-stats-table">
                          <tr className="team-stats-table-header-row">
                               <th className="team-stats-table-headers">PPG </th>
                               <th className="team-stats-table-headers">RB </th>
                               <th className="team-stats-table-headers">AST </th>
                               <th className="team-stats-table-headers">STL</th>
                               <th className="team-stats-table-headers">OFF </th>
                               <th className="team-stats-table-headers">DEF </th>
                          </tr>
                          <tr className="team-stats-table-data-row">   
                                <td className="team-stats-table-data">25.4</td>
                                <td className="team-stats-table-data">43.2</td>
                                <td className="team-stats-table-data">18.7</td>
                                <td className="team-stats-table-data">7.9</td>
                                <td className="team-stats-table-data">110.5</td>
                                <td className="team-stats-table-data">102.3</td>
                          </tr>

                  </table>

             </div>
             <img className="team-image" src={phili} alt="Profile" />
             <li className='team-nav-item'><h2>Philadephia <span>76ers</span> </h2></li>
      </div>
      <Sidebar/>
      <Main/>

      {/* <ProfileCard/> */}
    </div>
  )
}

export default App
