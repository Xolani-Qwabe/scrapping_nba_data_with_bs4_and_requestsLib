import React from 'react'
import ProfileCard from './ProfileCard';
import buddyHieldImage from './Buddy Hield.avif'; 
import joelEmbidImage from './Joel Embiid.avif'; 
import kellyOubreJrImage from './Kelly Oubre Jr.avif'; 
import tobiasHarrisImage from './Tobias Harris.avif'; 
import tyreseMaxeyImage from './Tyrese Maxey.avif'; 


function TeamCard(props){
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

    return <div className='team-container'>
          <div className='card-nav'>
            <ul className='team-card-nav'>
                <li className='team-card-nav-item'><button >Starters</button></li>
                <li className='team-card-nav-item'><button >Bench</button></li>
                <li className='team-card-nav-item'><button>PG</button></li>
                <li className='team-card-nav-item'><button>SG</button></li>
                <li className='team-card-nav-item'><button>SF</button></li>
                <li className='team-card-nav-item'><button>PF</button></li>
                <li className='team-card-nav-item'><button>C</button></li>
            </ul>
          </div>
          <div className='player-cards'>
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
        </div>

}


export default TeamCard;