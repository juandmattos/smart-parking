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
          <div className={classes.boxName}>
            <a 
              href='https://www.linkedin.com/in/pedrojesusbonillovalero-3933b4152/' 
              target='_blank' 
              rel='noreferrer'
              style={{ textDecoration: 'none', cursor: 'pointer', color: 'white' }}
            >
              Pedro Bonillo
            </a>
          </div>
          <div className={classes.box}>265075</div>
          <div className={classes.box}>pedrobonillo15@gmail.com</div>
          <div className={classes.boxName}>
            <a 
              href='https://www.linkedin.com/in/jos%C3%A9-d%C3%ADaz-baraibar-74b7a1113/' 
              target='_blank' 
              rel='noreferrer'
              style={{ textDecoration: 'none', cursor: 'pointer', color: 'white' }}
            >
              José Díaz
            </a>
          </div>
          <div className={classes.box}>230253</div>
          <div className={classes.box}>diazjose_80@hotmail.com</div>
          <div className={classes.boxName}>
            <a 
              href='https://www.linkedin.com/in/juan-diego-mattos-a6664793/' 
              target='_blank' 
              rel='noreferrer'
              style={{ textDecoration: 'none', cursor: 'pointer', color: 'white' }}
            >
              Juan Diego Mattos
            </a>
          </div>
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
