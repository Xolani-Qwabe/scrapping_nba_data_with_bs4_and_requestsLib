import React from 'react';


const ProfileCard = ({ name, img_path, position }) => {
  return (
    <div className="player-card">
      <img className="player-card-image" src={img_path} alt="Profile" />
      <div className="player-card-body">
        <h5 className="player-card-name">{name}</h5>
        <h5 className="player-card-position">{position}</h5>
        <button className='player-card-stats-button'>Player Stats</button>
      </div>
    </div>
  );
};

export default ProfileCard;
