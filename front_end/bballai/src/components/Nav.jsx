import React from 'react'

function Nav({nav_list}){
    // console.log(props)
    return <nav className='nav-component'>
        <h2 className='logo'>Bball AI</h2>
        <ul>
            {
                nav_list.map((item,index)=><li key={index}>{item}</li>)
            }     
        </ul>
    </nav>
   
}


export default Nav;