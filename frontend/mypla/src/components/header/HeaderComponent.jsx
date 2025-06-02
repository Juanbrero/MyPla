import './headerStyle.css'; // si tenés estilos para el header
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';

const apiServerUrl = import.meta.env.VITE_API_SERVER_URL;

export const HeaderComponent = () => {

    const select = () => {

    }

    const showHideMenu = () => {

    }

    return (
        <div className="header-container">
            <header>
                <div className="logo">
                    <Link to="/">MiPla</Link>
                </div>
                <nav>
                    <ul className="nav-list">
                        <li><Link to="/">Inicio</Link></li>
                        <li><Link to="/profile">Perfil</Link></li>
                        <li><Link to="/c2">Mi agenda</Link></li>
                    </ul>
                </nav>
                <div className="nav-responsive" onClick={showHideMenu}>
                    <FontAwesomeIcon icon={faBars} />
                </div>
            </header>
        </div>
    );
};

