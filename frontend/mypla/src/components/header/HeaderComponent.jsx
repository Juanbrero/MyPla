import './headerStyle.css'; // si tenés estilos para el header
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';

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

    return (
        <div className="header-container">
            <header>
                <div className="logo">
                    <Link to="/">MiPla</Link>
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

