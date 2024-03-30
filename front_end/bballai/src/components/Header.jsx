import React from 'react'

function Header({nav_list}){
    // console.log(props)
    return <nav className='header-component'>
        <h2 className='title'>BBallAI</h2>
        <ul>
            {
                nav_list.map((item,index)=><li key={index}>{item}</li>)
            }     
        </ul>
    </nav>
   
}


export default Header;