import './headerStyle.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';
import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getTopics } from '../../services/topics/topics.service';
import { LoginButton } from '../auth0Buttons/LoginButton';
import { SignupButton } from '../auth0Buttons/SignUpButton';
import { LogoutButton } from '../auth0Buttons/LogoutButton';
import { getCategories } from '../../services/categories/category.service';


export const HeaderComponent = ({token, roles}) => {
    let menuVisible = false;
    const [topics, setTopics] = useState([]);
    const [selectedTopic, setSelectedTopic] = useState('');
    const [searchByCategory, setSearchByCategory] = useState(false);
    const [categories, setCategories] = useState([]);
 

    useEffect(() => {
        const fetchTopics = async () => {
            try {
                const fetchedTopics = (await getTopics()).data;
                setTopics(fetchedTopics);
            } catch (error) {
                console.error('Error al obtener los tópicos:', error);
            }
        };

        fetchTopics();
    }, []);

    useEffect(() => {
        if (searchByCategory) {
            const fetchCategories = async () => {
                try {
                    const response = await getCategories();
                    const fetchedCategories = await response.data;
                    setCategories(fetchedCategories);
                } catch (error) {
                    console.error('Error al obtener las categorías:', error);
                }
            };

            fetchCategories();
        }
    }, [searchByCategory]);


    const showHideMenu = () => {
        const nav = document.getElementById("nav");
        if (menuVisible) {
            nav.classList = "";
        } else {
            nav.classList = "responsive";
        }
        menuVisible = !menuVisible;
    };

    const select = () => {
        document.getElementById("nav").classList = "";
        menuVisible = false;
    };

    const navigate = useNavigate();


    const search = () => {
        if (!selectedTopic) return;

        if (searchByCategory) {
            navigate(`/topicsList?category=${encodeURIComponent(selectedTopic)}`);
        } else {
            navigate(`/ProfessionalsList?topic=${encodeURIComponent(selectedTopic)}`);
        }
    };

    
    return (
        <div className="header-container">
            <header>
                <div className="logo">
                    <Link to="/">MiPla</Link>
                </div>
                {roles && roles.includes('Alumno') &&
                <div className="search-container">

                    <div className='search-filter'>
                        <label className='label-check-filter'>
                            <input
                                id='filter-checkbox' 
                                type='checkbox'
                                checked={searchByCategory}
                                onChange={(e) => {
                                    setSearchByCategory(e.target.checked);
                                    setSelectedTopic(''); // limpiar selección anterior
                                }}
                            >
                            </input>
                            <span>Buscar por categoria</span>
                        </label>
                    </div>

                    <div className='search-input-container'>
                        <div className="search-input">
                            <select
                                value={selectedTopic}
                                onChange={(e) => setSelectedTopic(e.target.value)}
                            >
                            <option value="">
                                {searchByCategory ? 'Seleccionar categoría...' : 'Seleccionar tópico...'}
                            </option>
                            {(searchByCategory ? categories : topics).map((item, index) => (
                                <option key={index} value={item}>
                                    {item}
                                </option>
                            ))}

                            </select>
                        </div>
                        <div className="search-icon">
                            <button id="search-button" onClick={search}>
                            {/* <button id="search-button" onClick={searchProfs}> */}
                                <FontAwesomeIcon icon={faMagnifyingGlass} />
                            </button>
                        </div>
                    </div>
                </div>
                }
                <div>
                    <nav id="nav">
                            {!token ? 
                              <ul className="nav-list">
                                  <li><Link to="/" onClick={select}>Inicio</Link></li>
                                  <LoginButton/>
                                  <SignupButton/>
                              </ul>
                              :
                                roles?.includes("Administrador") ? (
                                <ul className="nav-list">
                                    <li><Link to="/" onClick={select}>Inicio</Link></li>
                                    <li><Link to="/profile" onClick={select}>Perfil</Link></li>
                                    <li><Link to="/admin-topics" onClick={select}>Tópicos</Link></li>
                                    <li><Link to="/adminTransactions" onClick={select}>Transacciones</Link></li>
                                    <LogoutButton />
                                </ul>
                                ) : (
                                <ul className="nav-list">
                                    <li><Link to="/" onClick={select}>Inicio</Link></li>
                                    <li><Link to="/profile" onClick={select}>Perfil</Link></li>
                                    <li><Link to="/calendar" onClick={select}>Mi agenda</Link></li>
                                    <LogoutButton />
                                </ul>
                                )
                            }
                                            
                    </nav>
                    <div className="nav-responsive" onClick={showHideMenu}>
                        <FontAwesomeIcon icon={faBars} />
                    </div>
                </div>
            </header>
        </div>
    );
};
