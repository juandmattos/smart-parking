import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SpotItem from './SpotItem'
import Card from '../UI/Card'
import classes from './LevelList.module.css'
import { getIndividualParking } from '../../api/apiParking'

const LevelList = props => {
  const [levels, setLevels] = useState([])

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await getIndividualParking(props.parkingId)
        setLevels(response.data.levels)
      } catch (error) {
        console.log(error)
      }
    }
    fetch()
  }, [])

  console.log(levels)

  // useEffect(() => {
  //   const fetch = async () => {
  //     try {
  //       const response = await getIndividualParking(props.parkingId)
  //       setLevels(response.data.levels)
  //     } catch (error) {
  //       console.log(error)
  //     }
  //   }
  //   const interval = setInterval(() => fetch(), 5000);
  //   return () => clearInterval(interval);
  // }, [])

  return (
    <>
      <section className={classes.centered}>
        <h1>Pisos del Parking</h1>
        <Link 
          to={`/`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >        
          <p className={classes.back}>
            {`< Volver`}
          </p>
        </Link>
      </section>
      <section className={classes.spots}>
        <Card>
          <div>
            <div className={classes.container}>
              {levels.map((ele, index) => (
                <p key={index}>LEVEL ITEMS</p>
              ))}
            </div>
          </div>
        </Card>
      </section>
    </>
  )
}

export default LevelList
