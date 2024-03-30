import React from 'react';


const ProfileCard = ({ name, img_path, points }) => {
  return (
    <div className="player-card">
      {/* <p> PG 15.2</p>
      <p> AST 2.1</p>
      <p>RB 3.8</p> */}
      <img className="player-card-image" src={img_path} alt="Profile" />
      <div className="player-card-body">
        <h6 className="player-card-name">{name}</h6>
        <h5 className="player-card-position"> pts {points}</h5>
        <button className='player-card-stats-button'>Stats</button>
      </div>
    </div>
  );
};

export default ProfileCard;
