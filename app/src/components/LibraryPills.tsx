import { memo } from 'react';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';

interface Implementation {
  library_id: string;
  library_name: string;
  quality_score: number | null;
}

interface LibraryPillsProps {
  implementations: Implementation[];
  selectedLibrary: string;
  onSelect: (libraryId: string) => void;
}

export const LibraryPills = memo(function LibraryPills({
  implementations,
  selectedLibrary,
  onSelect,
}: LibraryPillsProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        gap: 1,
        justifyContent: 'center',
        py: 2,
        overflowX: 'auto',
        overflowY: 'hidden',
        mx: -2,
        px: 2,
        // Hide scrollbar but keep functionality
        scrollbarWidth: 'none',
        '&::-webkit-scrollbar': { display: 'none' },
      }}
    >
      {implementations.map((impl) => {
        const isSelected = impl.library_id === selectedLibrary;
        const score = impl.quality_score;

        return (
          <Chip
            key={impl.library_id}
            label={impl.library_id}
            onClick={() => onSelect(impl.library_id)}
            variant={isSelected ? 'filled' : 'outlined'}
            sx={{
              flexShrink: 0,
              fontFamily: '"MonoLisa", monospace',
              fontSize: '0.875rem',
              fontWeight: isSelected ? 600 : 400,
              bgcolor: isSelected ? '#3776AB' : 'transparent',
              color: isSelected ? '#fff' : '#6b7280',
              borderColor: isSelected ? '#3776AB' : '#d1d5db',
              '&:hover': {
                bgcolor: isSelected ? '#2c5f8a' : '#f3f4f6',
                borderColor: '#3776AB',
              },
              transition: 'all 0.15s ease',
              // Show quality score as subtle indicator
              '&::after': score ? {
                content: `"${Math.round(score)}"`,
                fontSize: '0.65rem',
                ml: 0.5,
                opacity: 0.7,
              } : undefined,
            }}
          />
        );
      })}
    </Box>
  );
});
