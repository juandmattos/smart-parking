import { Link } from 'react-router-dom'
import classes from './About.module.css'


function About() {
  return (
    <section  className={classes.centered}>
      <div className={classes.about}>
        <h1>About this project</h1>
        <p>Web App para visualizar informacion en tiempo real de distintos parkings</p>
        <p>Version: 1.0.0</p>
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
