import React from 'react'
const LoadingScreen = () => {
    const ball_img = ["basketball1.png", "soccer1.png", "baseball1.png"];
    const descriptors = ["freshest", "juiciest", "best", "hottest"]
    let loader = ball_img[Math.floor(Math.random() * ball_img.length)];
    let descriptor = descriptors[Math.floor(Math.random() * descriptors.length)];
  return (
    <div className="flex flex-col justify-center items-center py-20 space-y-4">
        <img
            src={`../../public/${loader}`}
            alt="Loading"
            className="w-36 h-36 animate-spin"
            />
        <span><h1 className='text-lg'>{`Finding the ${descriptor} arbs for you`}</h1></span>
        <span className="loading loading-dots loading-md"></span>
    </div>
  )
}

export default LoadingScreen