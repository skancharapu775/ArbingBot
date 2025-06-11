import React from 'react'
import ArbCard from './ArbCard'

const ArbList = ({arbs}) => {
  return (
    <>
    {arbs.map((arb, index) => (
      <ArbCard key={index} arb={arb} />
    ))}
    </>
  )
}

export default ArbList