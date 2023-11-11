#include <range/v3/all.hpp>
#include <AUI/View/ARadioButton.h>
#include <AUI/View/ARadioGroup.h>
#include <AUI/Model/AListModel.h>
#include "AUI/ASS/Property/BackgroundSolid.h"
#include "AUI/ASS/Property/Border.h"
#include "AUI/ASS/Property/TransformOffset.h"
#include "AUI/ASS/Selector/on_state.h"
#include "AUI/Layout/AVerticalLayout.h"
#include "AUI/Model/ATreeModel.h"
#include "AUI/View/A2FingerTransformArea.h"
#include "AUI/View/AButton.h"
#include "AUI/Layout/AHorizontalLayout.h"
#include "AUI/Platform/ACustomCaptionWindow.h"
#include "AUI/View/ACircleProgressBar.h"
#include "AUI/View/ALabel.h"
#include "AUI/Layout/AStackedLayout.h"
#include "AUI/View/ATextField.h"
#include "AUI/View/ASpacerExpanding.h"
#include "AUI/Util/UIBuildingHelpers.h"
#include "AUI/View/ASpinnerV2.h"
#include "AUI/View/AGroupBox.h"
#include "AUI/Util/ALayoutInflater.h"
#include "AUI/View/ASlider.h"
#include "AUI/Platform/APlatform.h"
#include "AUI/IO/AByteBufferInputStream.h"
#include "AUI/View/ASpinnerV2.h"
#include <AUI/i18n/AI18n.h>
#include <AUI/i18n/AI18n.h>
#include <AUI/ASS/ASS.h>
#include <AUI/View/ATextArea.h>
#include <AUI/View/ARulerView.h>
#include <AUI/View/AForEachUI.h>
#include <AUI/View/ARulerArea.h>
#include <AUI/Platform/ADesktop.h>
#include <AUI/Platform/AMessageBox.h>
#include <AUI/View/ASplitter.h>
#include <AUI/View/AScrollArea.h>
#include <AUI/View/ATabView.h>
#include <AUI/View/AGridSplitter.h>
#include <AUI/View/AText.h>
#include <AUI/View/ADrawableView.h>
#include <AUI/Traits/platform.h>

#include <memory>
#include <random>

#include "Window.h"

using namespace declarative;

ExampleWindow::ExampleWindow() : AWindow("Examples", 800_dp, 700_dp) {
    allowDragNDrop();

    setLayout(std::make_unique<AVerticalLayout>());
    AStylesheet::global().addRules({ {
        c(".all_views_wrap") > t<AViewContainer>(),
        Padding { 16_dp },
    } });

    addView(
        Horizontal {
            GroupBox {
                Label { "File" },
                Vertical {
                    _new<AButton>("Create file"),
                    _new<AButton>("Save file"),
                    _new<AButton>("Open file")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     mAsync << ADesktop::browseForFile(this).onSuccess([&](const APath& f) {
                                         if (f.empty()) {
                                             AMessageBox::show(this, "Result", "Cancelled");
                                         } else {
                                             AMessageBox::show(this, "Result", "File: {}"_format(f));
                                         }
                                     });
                                 }),
                    _new<AButton>("Save file as")
                        .connect(&AView::clicked, this,
                                 [&] {
                                     mAsync << ADesktop::browseForFile(this).onSuccess([&](const APath& f) {
                                         if (f.empty()) {
                                             AMessageBox::show(this, "Result", "Cancelled");
                                         } else {
                                             AMessageBox::show(this, "Result", "File: {}"_format(f));
                                         }
                                     });
                                 }),
                } with_style { MinSize { 200_dp } },
            },

            GroupBox {
                Label { "Fields" },
                Vertical {
                    Label { "Text area" },
                    _new<ATextArea>() with_style { 
                        FontSize { 12_pt },
                        Expanding {},
                        BackgroundSolid { AColor::WHITE }
                    },
                } with_style { Expanding {} },
            } with_style { MinSize { 200_dp }, Expanding {} },
        } with_style { Expanding {}, MinSize { 300_dp } }
    );
    //  AText::fromString("") with_style { ATextAlign::JUSTIFY },} with_style { MinSize { 200_dp } },
    //  AText::fromString("", { WordBreak::BREAK_ALL }),} with_style { MinSize { 200_dp } },

    addView(Horizontal {
        _new<ASpacerExpanding>(),
        _new<ALabel>("\u00a9 MironBerch, 2025") let {
            it << "#copyright";
            it->setEnabled(false);
        },
    });
}
