"""
Basic test file to verify project structure and functionality
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_project_structure():
    """Test that the project structure is correct"""
    project_root = Path(__file__).parent.parent
    
    # Check main directories exist
    assert (project_root / "src").exists()
    assert (project_root / "data").exists()
    assert (project_root / "docs").exists()
    assert (project_root / "tests").exists()
    assert (project_root / "dashboards").exists()
    assert (project_root / "assets").exists()
    
    # Check ETL structure
    assert (project_root / "src" / "etl").exists()
    assert (project_root / "src" / "etl" / "extract").exists()
    assert (project_root / "src" / "etl" / "transform").exists()
    assert (project_root / "src" / "etl" / "load").exists()
    assert (project_root / "src" / "etl" / "utils").exists()
    
    # Check data structure
    assert (project_root / "data" / "raw").exists()
    assert (project_root / "data" / "dimensional").exists()

def test_config_import():
    """Test that configuration can be imported"""
    try:
        from src.config import settings
        assert settings.PROJECT_ROOT.exists()
        assert settings.DATA_DIR.exists()
        assert settings.SRC_DIR.exists()
    except ImportError as e:
        pytest.fail(f"Failed to import settings: {e}")

def test_assets_exist():
    """Test that required assets exist"""
    project_root = Path(__file__).parent.parent
    assets_dir = project_root / "assets"
    
    assert (assets_dir / "dashboard.png").exists()
    assert (assets_dir / "kimball_star_model.png").exists()

def test_dashboard_file():
    """Test that dashboard file exists"""
    project_root = Path(__file__).parent.parent
    dashboard_file = project_root / "dashboards" / "Marketingdata.pbix"
    
    assert dashboard_file.exists()

def test_documentation_exists():
    """Test that documentation files exist"""
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs"
    
    assert (docs_dir / "data_dictionary.csv").exists()
    assert (docs_dir / "powerbi_setup.md").exists()
    assert (docs_dir / "api_docs.md").exists()

if __name__ == "__main__":
    pytest.main([__file__]) 