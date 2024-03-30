import React from 'react'
import ProfileCard from './ProfileCard';
import buddyHieldImage from './Buddy Hield.avif'; 

function Sidebar(props){
    const userData = {
        name:'Buddy Heild',
        points: "15.7",
        img_path: buddyHieldImage
      };

    return <aside className='sidebar-component'>
       <div>
            <ProfileCard
                name={userData.name}
                points={userData.points}
                img_path={userData.img_path}
            />
        </div>
    </aside>
}


export default Sidebar;