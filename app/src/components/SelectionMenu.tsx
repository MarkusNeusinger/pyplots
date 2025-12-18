import { useState, useRef } from 'react';
import Box from '@mui/material/Box';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import { LIBRARIES } from '../constants';

interface SelectionMenuProps {
  anchorEl: HTMLElement | null;
  open: boolean;
  onClose: () => void;
  viewMode: 'spec' | 'library';
  sortedSpecs: string[];
  selectedSpec?: string;
  selectedLibrary: string;
  onSelectSpec: (spec: string) => void;
  onSelectLibrary: (library: string) => void;
  onTrackEvent?: (name: string, props?: Record<string, string | undefined>) => void;
}

export function SelectionMenu({
  anchorEl,
  open,
  onClose,
  viewMode,
  sortedSpecs,
  selectedLibrary,
  onSelectSpec,
  onSelectLibrary,
  onTrackEvent,
}: SelectionMenuProps) {
  const [searchFilter, setSearchFilter] = useState('');
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const menuItemRefs = useRef<(HTMLLIElement | null)[]>([]);

  const handleClose = () => {
    onClose();
    setSearchFilter('');
    setHighlightedIndex(0);
  };

  const handleSelectSpec = (spec: string) => {
    onSelectSpec(spec);
    onTrackEvent?.('menu_select', { mode: 'spec', value: spec });
    handleClose();
  };

  const handleSelectLibrary = (library: string) => {
    onSelectLibrary(library);
    onTrackEvent?.('menu_select', { mode: 'library', value: library });
    handleClose();
  };

  const filteredSpecs = sortedSpecs.filter((spec) =>
    spec.toLowerCase().includes(searchFilter.toLowerCase())
  );

  const filteredLibraries = LIBRARIES.filter((lib) =>
    lib.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <Menu
      anchorEl={anchorEl}
      open={open}
      onClose={handleClose}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'center',
      }}
      transformOrigin={{
        vertical: 'top',
        horizontal: 'center',
      }}
      autoFocus={false}
      disableAutoFocus
      disableEnforceFocus
      TransitionProps={{
        onEntered: () => {
          // Don't auto-focus on touch devices to avoid keyboard popup
          const isTouchDevice = window.matchMedia('(hover: none)').matches;
          if (!isTouchDevice) {
            searchInputRef.current?.focus();
          }
        },
      }}
      PaperProps={{
        sx: {
          mt: 1,
          maxHeight: 350,
          minWidth: 220,
          fontFamily: '"JetBrains Mono", monospace',
        },
      }}
    >
      <Box sx={{ px: 1.5, py: 1, position: 'sticky', top: 0, bgcolor: '#fff', zIndex: 1 }}>
        <TextField
          size="small"
          placeholder="search..."
          value={searchFilter}
          onChange={(e) => {
            setSearchFilter(e.target.value);
            setHighlightedIndex(0);
          }}
          onKeyDown={(e) => {
            const filtered = viewMode === 'spec' ? filteredSpecs : filteredLibraries;

            if (e.key === 'Escape') {
              handleClose();
              return;
            }
            if (e.key === 'ArrowDown') {
              e.preventDefault();
              const newIndex = filtered.length > 0 ? (highlightedIndex + 1) % filtered.length : 0;
              setHighlightedIndex(newIndex);
              menuItemRefs.current[newIndex]?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
              return;
            }
            if (e.key === 'ArrowUp') {
              e.preventDefault();
              const newIndex = filtered.length > 0 ? (highlightedIndex - 1 + filtered.length) % filtered.length : 0;
              setHighlightedIndex(newIndex);
              menuItemRefs.current[newIndex]?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
              return;
            }
            // Stop propagation for all other keys (including letters) to prevent Menu from handling them
            e.stopPropagation();
            if (e.key === 'Enter') {
              if (filtered.length > 0 && highlightedIndex < filtered.length) {
                if (viewMode === 'spec') {
                  handleSelectSpec(filtered[highlightedIndex]);
                } else {
                  handleSelectLibrary(filtered[highlightedIndex]);
                }
              }
            }
          }}
          inputRef={searchInputRef}
          fullWidth
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon sx={{ fontSize: 18, color: '#9ca3af' }} />
              </InputAdornment>
            ),
            sx: {
              fontSize: '0.85rem',
              fontFamily: '"JetBrains Mono", monospace',
            },
          }}
        />
      </Box>
      {viewMode === 'spec' ? (
        filteredSpecs.map((spec, index) => (
          <MenuItem
            key={spec}
            ref={(el) => { menuItemRefs.current[index] = el; }}
            onClick={() => handleSelectSpec(spec)}
            onMouseEnter={() => setHighlightedIndex(index)}
            sx={{
              fontSize: '0.85rem',
              fontFamily: '"JetBrains Mono", monospace',
              bgcolor: index === highlightedIndex ? '#e8f4fc' : 'transparent',
              '&:hover': {
                bgcolor: '#e8f4fc',
              },
            }}
          >
            {spec}
          </MenuItem>
        ))
      ) : (
        filteredLibraries.map((lib, index) => (
          <MenuItem
            key={lib}
            ref={(el) => { menuItemRefs.current[index] = el; }}
            onClick={() => handleSelectLibrary(lib)}
            onMouseEnter={() => setHighlightedIndex(index)}
            sx={{
              fontSize: '0.85rem',
              fontFamily: '"JetBrains Mono", monospace',
              bgcolor: lib === selectedLibrary || index === highlightedIndex ? '#e8f4fc' : 'transparent',
              '&:hover': {
                bgcolor: '#e8f4fc',
              },
            }}
          >
            {lib}
          </MenuItem>
        ))
      )}
    </Menu>
  );
}
