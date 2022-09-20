import classes from './Summary.module.css'

const Summary = () => {
  return (
    <section className={classes.summary}>
      <h2>Parking App</h2>
      <p>
        Parking App es un proyecto con el objetivo de consumir datos de distintos parkings e informar en tiempo real el estado de cada lugar de estacionamiento de los parkings.
      </p>
      <br />
      <p>
        A continuación se despliega la información de todos los estacionamientos en el sistema. Cada uno se puede desglozar en conceptos generales, lugares de estacionamiento, estado de los mismos y precio actual.
      </p>
    </section>
  )
}

export default Summary
