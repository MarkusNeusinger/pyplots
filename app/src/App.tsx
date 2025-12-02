import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import ShuffleIcon from '@mui/icons-material/Shuffle';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const GITHUB_URL = 'https://github.com/MarkusNeusinger/pyplots';

interface PlotImage {
  library: string;
  url: string;
}

function App() {
  const [specs, setSpecs] = useState<string[]>([]);
  const [selectedSpec, setSelectedSpec] = useState<string>('');
  const [images, setImages] = useState<PlotImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  // Shuffle to a different random spec
  const shuffleSpec = () => {
    if (specs.length <= 1) return;
    const otherSpecs = specs.filter((s) => s !== selectedSpec);
    const randomIndex = Math.floor(Math.random() * otherSpecs.length);
    setSelectedSpec(otherSpecs[randomIndex]);
  };

  // Load specs on mount
  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const response = await fetch(`${API_URL}/specs`);
        if (!response.ok) throw new Error('Failed to fetch specs');
        const data = await response.json();
        setSpecs(data.specs);

        // Select random spec
        if (data.specs.length > 0) {
          const randomIndex = Math.floor(Math.random() * data.specs.length);
          setSelectedSpec(data.specs[randomIndex]);
        }
      } catch (err) {
        setError(`Error loading specs: ${err}`);
      }
    };

    fetchSpecs();
  }, []);

  // Load images when spec changes
  useEffect(() => {
    if (!selectedSpec) {
      setLoading(false);
      return;
    }

    const fetchImages = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${API_URL}/specs/${selectedSpec}/images`);
        if (!response.ok) throw new Error('Failed to fetch images');
        const data = await response.json();
        setImages(data.images);
      } catch (err) {
        setError(`Error loading images: ${err}`);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, [selectedSpec]);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: '#fff',
        py: 6,
      }}
    >
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Link
            href="https://pyplots.ai"
            target="_blank"
            rel="noopener noreferrer"
            underline="none"
          >
            <Typography
              variant="h2"
              component="h1"
              sx={{
                fontWeight: 700,
                color: '#1f2937',
                mb: 3,
                letterSpacing: '-0.02em',
              }}
            >
              pyplots.ai
            </Typography>
          </Link>

          <Typography
            variant="body1"
            sx={{
              maxWidth: 640,
              mx: 'auto',
              lineHeight: 1.8,
              mb: 3,
              color: '#6b7280',
              fontSize: '1.05rem',
            }}
          >
            An AI-powered platform for Python data visualization that automatically discovers,
            generates, tests, and maintains plotting examples across matplotlib, seaborn, plotly,
            bokeh, altair, plotnine, pygal, and highcharts.
          </Typography>

          <Chip
            label="Early Preview"
            variant="outlined"
            size="small"
            sx={{
              borderColor: '#e5e7eb',
              color: '#9ca3af',
              fontWeight: 500,
              fontSize: '0.75rem',
            }}
          />
        </Box>

        {/* Error Display */}
        {error && (
          <Alert severity="error" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
            {error}
          </Alert>
        )}

        {/* Loading State */}
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
            <CircularProgress size={40} sx={{ color: '#d1d5db' }} />
          </Box>
        )}

        {/* Content */}
        {!loading && selectedSpec && (
          <Box>
            {/* Spec Title with Shuffle */}
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 2,
                mb: 5,
              }}
            >
              <Typography
                variant="body2"
                sx={{
                  color: '#9ca3af',
                  textTransform: 'uppercase',
                  letterSpacing: 2,
                  fontSize: '0.7rem',
                  fontWeight: 500,
                }}
              >
                Random Example
              </Typography>

              <Chip
                label={selectedSpec}
                variant="outlined"
                sx={{
                  fontSize: '0.95rem',
                  fontWeight: 600,
                  color: '#374151',
                  borderColor: '#e5e7eb',
                  bgcolor: '#f9fafb',
                  py: 2,
                  px: 0.5,
                }}
              />

              <IconButton
                onClick={shuffleSpec}
                size="small"
                sx={{
                  color: '#9ca3af',
                  '&:hover': {
                    color: '#2563eb',
                    bgcolor: '#eff6ff',
                  },
                }}
                title="Show another example"
              >
                <ShuffleIcon fontSize="small" />
              </IconButton>
            </Box>

            {images.length === 0 ? (
              <Alert
                severity="info"
                sx={{
                  maxWidth: 400,
                  mx: 'auto',
                  bgcolor: '#f9fafb',
                  border: '1px solid #e5e7eb',
                  '& .MuiAlert-icon': { color: '#9ca3af' },
                }}
              >
                No images found for this spec.
              </Alert>
            ) : (
              <Grid container spacing={4} justifyContent="center">
                {images.map((img) => (
                  <Grid size={{ xs: 12, md: 6 }} key={img.library}>
                    <Box>
                      <Card
                        elevation={0}
                        sx={{
                          borderRadius: 4,
                          overflow: 'hidden',
                          border: '1px solid #f3f4f6',
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            borderColor: '#e5e7eb',
                            boxShadow: '0 4px 20px rgba(0,0,0,0.06)',
                          },
                        }}
                      >
                        <CardMedia
                          component="img"
                          image={img.url}
                          alt={`${selectedSpec} - ${img.library}`}
                          sx={{
                            width: '100%',
                            aspectRatio: '16 / 9',
                            objectFit: 'contain',
                            bgcolor: '#fff',
                          }}
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.style.display = 'none';
                          }}
                        />
                      </Card>
                      {/* Library label below card */}
                      <Typography
                        sx={{
                          mt: 1.5,
                          textAlign: 'center',
                          fontSize: '0.8rem',
                          fontWeight: 500,
                          color: '#9ca3af',
                          textTransform: 'lowercase',
                        }}
                      >
                        {img.library}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            )}
          </Box>
        )}

        {/* No specs available */}
        {!loading && specs.length === 0 && (
          <Alert severity="warning" sx={{ maxWidth: 400, mx: 'auto' }}>
            No specs found.
          </Alert>
        )}

        {/* Footer */}
        <Box sx={{ textAlign: 'center', mt: 10, pt: 6, borderTop: '1px solid #f3f4f6' }}>
          <Link
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            sx={{
              fontSize: '0.8rem',
              color: '#9ca3af',
              textDecoration: 'none',
              '&:hover': { color: '#6b7280' },
            }}
          >
            View on GitHub
          </Link>
        </Box>
      </Container>
    </Box>
  );
}

export default App;
