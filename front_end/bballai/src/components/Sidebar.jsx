import React from 'react'
import ProfileCard from './ProfileCard';
import buddyHieldImage from './Buddy Hield.avif'; 

function Sidebar(props){
    const userData = {
        name:'Buddy Heild',
        position: "Shooting Gaurd",
        img_path: buddyHieldImage
      };

    return <aside className='sidebar-component'>
       <div>
            <ProfileCard
                name={userData.name}
                position={userData.position}
                img_path={userData.img_path}
            />
        </div>
    </aside>
}


export default Sidebar;