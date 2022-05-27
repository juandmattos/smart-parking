import { useParams } from 'react-router-dom'
import SummaryParking from '../components/jparkings/SummaryParking'

const SummaryPage = () => {
  const { parkingId } = useParams()
  return (
    <SummaryParking parkingId={parkingId} />
  )
}

export default SummaryPage
