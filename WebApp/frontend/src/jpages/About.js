import { Link } from 'react-router-dom'
import classes from './About.module.css'


function About() {
  return (
    <section  className={classes.centered}>
      <div className={classes.about}>
        <h1>About this project</h1>
        <p>
          Web App para visualizar información en tiempo real de distintos parkings.
        </p>
        <p>
          Parte del proyecto de tesis del Mater de Big Data cursado en la universidad ORT en Montevideo, Uruguay
        </p>
        <p>
          Creada por:
        </p>
        <div className={classes.wrapper}>
          <div className={classes.boxName}>Pedro Bonillo</div>
          <div className={classes.box}>265075</div>
          <div className={classes.box}>pedrobonillo15@gmail.com</div>

          <div className={classes.boxName}>Jose Diaz</div>
          <div className={classes.box}>230253</div>
          <div className={classes.box}>diazjose_80@hotmail.com</div>

          <div className={classes.boxName}>Juan Diego Mattos</div>
          <div className={classes.box}>262316</div>
          <div className={classes.box}>juandmattos@gmail.com</div>
        </div>
        <Link 
          to={`/`}
          style={{
            color: 'inherit',
            textDecoration: 'inherit'
          }}
        >
          {`< Volver`}
        </Link>
      </div>
    </section>
  )
}

export default About
