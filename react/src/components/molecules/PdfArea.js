import React, {useState} from 'react';
import samplePDF from "../sample-data/samplepdf.pdf";
import {Page, Document} from "react-pdf/dist/esm/entry.webpack";
import {css} from "@emotion/react";
import PdfComment from "./PdfComment";

const TemplateStyle = css`
  background: coral;
  padding: 10px;
  .pdf-area{
    position: relative;
  }

  canvas {
    margin: auto;

  }
`

const BasicStyle = css`
  ${TemplateStyle};
`

function PdfArea(props) {
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    function onDocumentLoadSuccess({numPages}) {
        setNumPages(numPages);
        setPageNumber(1);
    }

    function changePage(offset) {
        setPageNumber(prevPageNumber => prevPageNumber + offset);
    }

    function previousPage() {
        changePage(-1);
    }

    function nextPage() {
        changePage(1);
    }


    return (
        <div className={'content-area'} css={BasicStyle}>
            <div className={'pdf-area'}
            >

                <Document
                    file={samplePDF}
                    options={{
                        cMapUrl: 'https://localhost/cmaps/',
                        cMapPacked: true,
                    }}
                    onLoadSuccess={onDocumentLoadSuccess}
                >

                    <Page pageNumber={pageNumber}/>
                </Document>
                <PdfComment pageNumber={pageNumber}/>

            </div>
            <div>
                <p>
                    Page {pageNumber || (numPages ? 1 : '--')} of {numPages || '--'}
                </p>
                <button
                    type="button"
                    disabled={pageNumber <= 1}
                    onClick={previousPage}
                >
                    Previous
                </button>
                <button
                    type="button"
                    disabled={pageNumber >= numPages}
                    onClick={nextPage}
                >
                    Next
                </button>
            </div>
        </div>

    )
}

export default PdfArea;