import React from 'react'

const AnimatedDots = () => {
    const [dots, setDots] = React.useState("");
  
    React.useEffect(() => {
      const interval = setInterval(() => {
        setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
      }, 500);
      return () => clearInterval(interval);
    }, []);
  
    return <span>{dots}</span>;
  };

export default AnimatedDots