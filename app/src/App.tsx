import { useState } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Stack from '@mui/material/Stack';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const fetchHello = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/hello/Frontend`);
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      setMessage('Error connecting to API');
      console.error('API Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
      }}
    >
      <Container maxWidth="sm">
        <Stack spacing={4}>
          <Typography variant="h2" component="h1" align="center" gutterBottom>
            🎨 pyplots
          </Typography>

          <Typography variant="h5" align="center" color="text.secondary" paragraph>
            AI-Powered Python Plotting Examples
          </Typography>

          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Hello World Demo
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Click the button below to test the connection to the FastAPI backend.
              </Typography>
              {message && (
                <Typography
                  variant="body1"
                  sx={{
                    mt: 2,
                    p: 2,
                    bgcolor: 'primary.light',
                    color: 'primary.contrastText',
                    borderRadius: 1,
                  }}
                >
                  {message}
                </Typography>
              )}
            </CardContent>
            <CardActions>
              <Button
                variant="contained"
                onClick={fetchHello}
                disabled={loading}
                fullWidth
                size="large"
              >
                {loading ? 'Loading...' : 'Test API Connection'}
              </Button>
            </CardActions>
          </Card>

          <Card variant="outlined">
            <CardContent>
              <Typography variant="body2" color="text.secondary">
                <strong>Stack:</strong> React 19 + TypeScript + Vite 7 + MUI 7
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>API:</strong> {API_URL}
              </Typography>
            </CardContent>
          </Card>
        </Stack>
      </Container>
    </Box>
  );
}

export default App;
