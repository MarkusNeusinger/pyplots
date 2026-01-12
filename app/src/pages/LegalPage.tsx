import { useEffect } from 'react';
import { Helmet } from 'react-helmet-async';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';

import { useAnalytics } from '../hooks';
import { Breadcrumb, Footer } from '../components';
import { GITHUB_URL } from '../constants';

export function LegalPage() {
  const { trackPageview, trackEvent } = useAnalytics();

  useEffect(() => {
    trackPageview('/legal');
  }, [trackPageview]);

  const headingStyle = {
    fontFamily: '"MonoLisa", monospace',
    fontWeight: 600,
    fontSize: '1rem',
    color: '#1f2937',
    mb: 2,
  };

  const subheadingStyle = {
    fontFamily: '"MonoLisa", monospace',
    fontWeight: 600,
    fontSize: '1.1rem',
    color: '#374151',
    mt: 3,
    mb: 1,
  };

  const textStyle = {
    fontFamily: '"MonoLisa", monospace',
    fontSize: '0.9rem',
    color: '#4b5563',
    lineHeight: 1.8,
    mb: 2,
  };

  const tableStyle = {
    '& .MuiTableCell-root': {
      fontFamily: '"MonoLisa", monospace',
      fontSize: '0.85rem',
      color: '#4b5563',
      borderBottom: '1px solid #f3f4f6',
      py: 1.5,
      px: 2,
    },
    '& .MuiTableCell-root:first-of-type': {
      fontWeight: 500,
      color: '#374151',
      width: '40%',
    },
  };

  return (
    <>
      <Helmet>
        <title>legal | pyplots.ai</title>
        <meta name="description" content="Legal notice, privacy policy, and transparency information for pyplots.ai" />
        <meta property="og:title" content="legal | pyplots.ai" />
        <meta property="og:description" content="Legal notice, privacy policy, and transparency information" />
      </Helmet>

      <Breadcrumb items={[{ label: 'pyplots.ai', to: '/' }, { label: 'legal' }]} sx={{ mb: 4 }} />

      <Box sx={{ pb: 4, maxWidth: 1100, mx: 'auto' }}>
        {/* Legal Notice */}
        <Paper component="section" id="legal-notice" sx={{ p: 3, mb: 2 }}>
          <Typography variant="h2" sx={headingStyle}>
            Legal Notice
          </Typography>

          <Typography sx={textStyle}>
            <strong>Operator</strong>
            <br />
            Markus Neusinger
            <br />
            Visp, Switzerland
          </Typography>

          <Typography sx={textStyle}>
            <strong>Contact</strong>
            <br />
            Email:{' '}
            <Link href="mailto:admin@pyplots.ai" sx={{ color: '#3776AB' }}>
              admin@pyplots.ai
            </Link>
          </Typography>

          <Typography sx={textStyle}>
            <strong>Disclaimer</strong>
            <br />
            This is a personal portfolio project, not a commercial service. The content is provided &quot;as is&quot;
            without warranty of any kind. Code examples are for educational purposes and should be reviewed before use
            in production environments.
          </Typography>
        </Paper>

        {/* Privacy Policy */}
        <Paper component="section" id="privacy" sx={{ p: 3, mb: 2 }}>
          <Typography variant="h2" sx={headingStyle}>
            Privacy Policy
          </Typography>

          <Typography sx={subheadingStyle}>Data Controller</Typography>
          <Typography sx={textStyle}>Markus Neusinger (see Legal Notice above)</Typography>

          <Typography sx={subheadingStyle}>What We Collect</Typography>
          <Typography sx={textStyle}>
            <strong>Anonymized Analytics</strong>: We use Plausible Analytics, a privacy-focused analytics tool. It
            collects no personal data, uses no cookies, and does not track you across websites. All data is aggregated
            and anonymous.
          </Typography>
          <Typography sx={textStyle}>
            <strong>Server Logs</strong>: Temporary technical logs (anonymized IP addresses) are retained for up to 30
            days for security and debugging purposes.
          </Typography>

          <Typography sx={subheadingStyle}>What We Do NOT Collect</Typography>
          <Typography sx={textStyle}>
            • No user accounts or personal profiles
            <br />
            • No personal data (names, emails, etc.)
            <br />
            • No cookies (except technically necessary session cookies)
            <br />• <strong>No AI training</strong>: Your interactions are not used to train AI models
          </Typography>

          <Typography sx={textStyle}>
            <strong>Analytics</strong>: Filter selections and search terms are tracked anonymously via Plausible
            Analytics for usage statistics. This data is aggregated and cannot be linked to individual users.
          </Typography>

          <Typography sx={textStyle}>
            <strong>Contributors</strong>: If you suggest a plot type via GitHub, your GitHub username may be credited
            in the specification metadata. This is public information from your GitHub profile.
          </Typography>

          <Typography sx={subheadingStyle}>Hosting &amp; Third Parties</Typography>
          <Typography sx={textStyle}>All services are hosted in the EU (Netherlands, europe-west4):</Typography>
          <Table sx={tableStyle}>
            <TableBody>
              <TableRow>
                <TableCell>Hosting</TableCell>
                <TableCell>Google Cloud Run (Netherlands)</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Database</TableCell>
                <TableCell>Google Cloud SQL (Netherlands)</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Storage</TableCell>
                <TableCell>Google Cloud Storage (Netherlands)</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Analytics</TableCell>
                <TableCell>Plausible Analytics (EU, proxied)</TableCell>
              </TableRow>
            </TableBody>
          </Table>

          <Typography sx={subheadingStyle}>Your Rights</Typography>
          <Typography sx={textStyle}>
            Under GDPR and Swiss DSG, you have the right to access, rectification, erasure, and data portability. Since
            we do not store personal data, there is typically nothing to delete or export. For questions, contact{' '}
            <Link href="mailto:admin@pyplots.ai" sx={{ color: '#3776AB' }}>
              admin@pyplots.ai
            </Link>
            .
          </Typography>
        </Paper>

        {/* Transparency */}
        <Paper component="section" id="transparency" sx={{ p: 3, mb: 2 }}>
          <Typography variant="h2" sx={headingStyle}>
            Transparency
          </Typography>

          <Typography sx={textStyle}>
            This project is open source and committed to full transparency about how it works and what it costs.
          </Typography>

          <Typography sx={subheadingStyle}>Technology Stack</Typography>
          <Table sx={tableStyle}>
            <TableBody>
              <TableRow>
                <TableCell>Typography</TableCell>
                <TableCell>
                  <Link href="https://www.monolisa.dev/" target="_blank" rel="noopener" sx={{ color: '#3776AB' }}>
                    MonoLisa
                  </Link>{' '}
                  by Marcus Sterz
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Frontend</TableCell>
                <TableCell>React 19, Vite, MUI 7, TypeScript</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Backend</TableCell>
                <TableCell>Python 3.13, FastAPI, SQLAlchemy</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Database</TableCell>
                <TableCell>PostgreSQL</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Hosting</TableCell>
                <TableCell>Google Cloud Run (Netherlands)</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Storage</TableCell>
                <TableCell>Google Cloud Storage</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Analytics</TableCell>
                <TableCell>Plausible (privacy-friendly, no cookies)</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>AI</TableCell>
                <TableCell>Anthropic Claude via Claude Max (code generation &amp; review)</TableCell>
              </TableRow>
            </TableBody>
          </Table>

          <Typography sx={subheadingStyle}>Source Code</Typography>
          <Typography sx={textStyle}>
            The entire codebase is publicly available under the MIT License:
            <br />
            <Link href={GITHUB_URL} target="_blank" rel="noopener" sx={{ color: '#3776AB' }}>
              github.com/MarkusNeusinger/pyplots
            </Link>
          </Typography>

          <Typography sx={subheadingStyle}>Monthly Costs (approximate)</Typography>
          <Table sx={tableStyle}>
            <TableBody>
              <TableRow>
                <TableCell>Cloud Run</TableCell>
                <TableCell>~$15</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Cloud SQL</TableCell>
                <TableCell>~$40</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Cloud Storage</TableCell>
                <TableCell>~$5</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Plausible Analytics</TableCell>
                <TableCell>~$9</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Domain (.ai)</TableCell>
                <TableCell>~$8</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Claude Max</TableCell>
                <TableCell>~$100 (shared)</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <strong>Total</strong>
                </TableCell>
                <TableCell>
                  <strong>~$177/month</strong>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
          <Typography sx={{ ...textStyle, fontSize: '0.8rem', color: '#9ca3af', mt: 1 }}>
            Claude Max subscription is shared across projects.
            <br />
            All costs are currently covered privately. Last updated: January 2026.
          </Typography>
        </Paper>
      </Box>

      <Footer onTrackEvent={trackEvent} />
    </>
  );
}
