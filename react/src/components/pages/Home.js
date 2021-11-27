import Header from "../organisms/Header.js";

const homeStyle = {
    display: 'flex',
    alignItems: 'center',
}

function HomePage(props){
    return (
        <div >
            <Header label={props.label}/>
            home
        </div>
    );
}
export default HomePage;
