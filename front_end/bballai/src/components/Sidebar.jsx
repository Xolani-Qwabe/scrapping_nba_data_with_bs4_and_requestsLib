import React from 'react'
import ProfileCard from './ProfileCard';
import buddyHieldImage from './Buddy Hield.avif'; 
import joelEmbidImage from './Joel Embiid.avif'; 
import kellyOubreJrImage from './Kelly Oubre Jr.avif'; 
import tobiasHarrisImage from './Tobias Harris.avif'; 
import tyreseMaxeyImage from './Tyrese Maxey.avif'; 

function Sidebar(props){
    const userData = [{
        name:'Tyrese Maxey',
        points: "25.6",
        img_path: tyreseMaxeyImage
      },{
        name:'Buddy Heild',
        points: "15.7",
        img_path: buddyHieldImage
      },{
        name:'Kelly Oubre Jr',
        points: "14.8",
        img_path: kellyOubreJrImage
      },{
        name:'Tobias Harris',
        points: "17.2",
        img_path: tobiasHarrisImage
      },{
        name:'Joel Embiid',
        points: "35.3",
        img_path: joelEmbidImage
      }];

    return <aside className='sidebar-component'>
       <div className='side-container'>
 
           <ul className='team-nav'>
                <li className='team-nav-item'><button >Staters</button></li>
                <li className='team-nav-item'><button >Reserves</button></li>
                <li className='team-nav-item'><button>Point Gaurds</button></li>
                <li className='team-nav-item'><button>Shooting Gaurds</button></li>
                <li className='team-nav-item'><button>Small Forwards</button></li>
                <li className='team-nav-item'><button>Power Forwards</button></li>
                <li className='team-nav-item'><button>Centers</button></li>
                
            </ul>
        
            <ProfileCard
                name={userData[0].name}
                points={userData[0].points}
                img_path={userData[0].img_path}
            />
            <ProfileCard
                name={userData[1].name}
                points={userData[1].points}
                img_path={userData[1].img_path}
            />
            <ProfileCard
                name={userData[2].name}
                points={userData[2].points}
                img_path={userData[2].img_path}
            />
            <ProfileCard
               name={userData[3].name}
               points={userData[3].points}
               img_path={userData[3].img_path}
            />
            <ProfileCard
                name={userData[4].name}
                points={userData[4].points}
                img_path={userData[4].img_path}
            />
          
        </div>
    </aside>
}


export default Sidebar;