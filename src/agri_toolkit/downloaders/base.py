"""Base downloader class for all data sources."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

from agri_toolkit.core.config import Config
from agri_toolkit.core.logger import get_logger

logger = get_logger()


class BaseDownloader(ABC):
    """Abstract base class for all data downloaders.
    
    All data source downloaders should inherit from this class and
    implement the download() method.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the downloader.
        
        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.logger = logger
        self._setup_directories()
    
    def _setup_directories(self) -> None:
        """Create necessary directories for data storage."""
        self.config.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.config.processed_data_path.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def download(self, **kwargs) -> Any:
        """Download data from the source.
        
        This method must be implemented by all subclasses.
        
        Args:
            **kwargs: Downloader-specific parameters.
        
        Returns:
            Downloaded data (format varies by downloader).
        
        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement download() method")
    
    def validate(self, data: Any) -> bool:
        """Validate downloaded data.
        
        Args:
            data: Data to validate.
        
        Returns:
            True if data is valid, False otherwise.
        """
        # Default implementation - can be overridden
        return data is not None
    
    def get_output_path(self, filename: str, subdirectory: Optional[str] = None) -> Path:
        """Get output path for downloaded data.
        
        Args:
            filename: Name of the output file.
            subdirectory: Optional subdirectory within raw data path.
        
        Returns:
            Path object for the output file.
        """
        if subdirectory:
            output_dir = self.config.raw_data_path / subdirectory
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir / filename
        
        return self.config.raw_data_path / filename
