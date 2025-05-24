import { useNavigate } from "react-router";
import { IoIosArrowBack } from "react-icons/io";

export default function Navigation({onClick, mode}) {
    const navigate = useNavigate();
    const handleGoBack = () => {
        navigate(-1);
    }
    return (
        <div className="navigation">
            <button className="go-back-action" onClick={handleGoBack}><IoIosArrowBack /> Go Back</button>
            <h4>New Template</h4>
            <button className="nav-action" onClick={onClick}>{mode === 'edit' ? 'Update Template' : 'Save Template'}</button>
        </div>
    )
}