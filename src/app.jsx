import { useState } from 'react'
import { Alert, Box } from '@mui/material'
import { Chatbot } from './chatbot/chatbot'
import { AppContext } from './util'
import { ErrorBoundary } from './error'

function App() {
  const [error, setError] = useState(null)

  return (
    <AppContext.Provider value={{ error, setError }}>
      <ErrorBoundary>
        <Box sx={{display: 'flex', flexDirection: 'column', height: '100vh'}}>
        {error && <Alert severity="error" onClose={() => setError(false)}>Sorry, there was an error</Alert>}
        <Chatbot />
        </Box>

      </ErrorBoundary>
    </AppContext.Provider>
  )
}

export default App
