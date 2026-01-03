import { useState, useEffect, createContext, useContext } from 'react';
import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

import { API_URL } from '../constants';
import type { LibraryInfo, SpecInfo } from '../types';

interface AppData {
  specsData: SpecInfo[];
  librariesData: LibraryInfo[];
  stats: { specs: number; plots: number; libraries: number } | null;
}

const AppDataContext = createContext<AppData | null>(null);

export function useAppData() {
  const context = useContext(AppDataContext);
  if (!context) {
    throw new Error('useAppData must be used within Layout');
  }
  return context;
}

export function Layout() {
  const [specsData, setSpecsData] = useState<SpecInfo[]>([]);
  const [librariesData, setLibrariesData] = useState<LibraryInfo[]>([]);
  const [stats, setStats] = useState<{ specs: number; plots: number; libraries: number } | null>(null);

  // Load shared data on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [specsRes, libsRes, statsRes] = await Promise.all([
          fetch(`${API_URL}/specs`),
          fetch(`${API_URL}/libraries`),
          fetch(`${API_URL}/stats`),
        ]);

        if (specsRes.ok) {
          const data = await specsRes.json();
          setSpecsData(Array.isArray(data) ? data : data.specs || []);
        }

        if (libsRes.ok) {
          const data = await libsRes.json();
          setLibrariesData(data.libraries || []);
        }

        if (statsRes.ok) {
          const data = await statsRes.json();
          setStats(data);
        }
      } catch (err) {
        console.error('Error loading initial data:', err);
      }
    };
    fetchData();
  }, []);

  return (
    <AppDataContext.Provider value={{ specsData, librariesData, stats }}>
      <Box sx={{ minHeight: '100vh', bgcolor: '#fafafa', py: 5, position: 'relative' }}>
        <Container maxWidth={false} sx={{ px: { xs: 2, sm: 4, md: 8, lg: 12 } }}>
          <Outlet />
        </Container>
      </Box>
    </AppDataContext.Provider>
  );
}
