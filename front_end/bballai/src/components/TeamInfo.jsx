import React from 'react'
import phili from './to_use.png'

function TeamInfo(props){
    // console.log(props)
    return (
        <div className='team-info'>
                 <div className=" team-stats-table-div">
                       <table className="team-stats-table">
                              <tr className="team-stats-table-header-row">
                                   <th className="team-stats-table-headers">PPG </th>
                                   <th className="team-stats-table-headers">RB </th>
                                   <th className="team-stats-table-headers">AST </th>
                                   <th className="team-stats-table-headers">OPPG </th>
                                   
                              </tr>
                              <tr className="team-stats-table-data-row">   
                                    <td className="team-stats-table-data">114.4</td>
                                    <td className="team-stats-table-data">42.7</td>
                                    <td className="team-stats-table-data">24.6</td>
                                    <td className="team-stats-table-data">112.2</td>
                              </tr>
    
                      </table>
    
                 </div>
                 <img className="team-image" src={phili} alt="Profile" />
                 <h2 className='team-name'>Philadephia <span>76ers</span> </h2>
          </div>
    )
}


export default TeamInfo;





