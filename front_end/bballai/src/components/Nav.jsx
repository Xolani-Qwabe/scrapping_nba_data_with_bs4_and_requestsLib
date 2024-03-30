import React from 'react'

function Nav({nav_list}){
    console.log(nav_list)
    return <div>
    <nav className='nav-component'>
        <ul>
            {
                nav_list.map((item,index)=><li key={index}>{item}</li>)
            }     
        </ul>
    </nav>
    </div>
}


export default Nav;