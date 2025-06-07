import './headerStyle.css'; // si tenés estilos para el header
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';



const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const HeaderComponent = () => {

    let menuVisible = false;

    const showHideMenu = () =>  {

        if(menuVisible) {
            document.getElementById("nav").classList = "";
            menuVisible = false;  
        }
        else {
            document.getElementById("nav").classList = "responsive";
            menuVisible = true;  
        }
    }

    const select = () => {
        document.getElementById("nav").classList = "";
        menuVisible = false;
    }

    const navigate = useNavigate();

    const searchProfs = async () => {
        const topic = $("#searchTopic").val();
        return navigate(`/ProfessionalsList?topic=${encodeURIComponent(topic)}`);
    }


    return (
        <div className="header-container">
            <header>
                <div className="logo">
                    <Link to="/">MiPla</Link>
                </div>
                <div className="search-container">
                    <div className="search-icon">
                        <button id='search-button' onClick={() => searchProfs()}>
                            <FontAwesomeIcon icon={faMagnifyingGlass} />
                        </button>
                    </div>
                    <div className="search-input">
                        <input id="searchTopic" type="text" placeholder='Buscar topicos...' />
                    </div>
                </div>
                <nav id="nav">
                    <ul className="nav-list">
                        <li><Link to="/" onClick={select}>Inicio</Link></li>
                        <li><Link to="/profile" onClick={select}>Perfil</Link></li>
                        <li><Link to="/calendar" onClick={select}>Mi agenda</Link></li>
                    </ul>
                </nav>
                <div className="nav-responsive" onClick={showHideMenu}>
                    <FontAwesomeIcon icon={faBars} />
                </div>
            </header>
        </div>
    );
};

